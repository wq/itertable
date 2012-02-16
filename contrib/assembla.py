from wq.io import XmlNetIO
from lxml import etree

# AssemblaIO
# a python implementation of
# http://www.assembla.com/spaces/breakoutdocs/wiki/Assembla_REST_API

class AssemblaIO(XmlNetIO):
    "Base class for accessing Assembla REST API"

    # NetIO headers
    headers  = {"Accept":       "application/xml",
                "Content-type": "application/xml"}

    # Assembla space ID (given as argument to constructor)
    space = None

    # Avoid creating alerts in stream/email (but DELETE will always create alerts)
    skip_alerts = True

    # NetIO url 
    @property
    def url(self):
        return "https://www.assembla.com/spaces/" + self.space
    
    def get_set_url(self, key):
        raise NotImplementedError
    
    def get_del_url(self, key):
        return self.get_set_url(key)
    
    def get_append_url(self):
        raise NotImplementedError
    
    # Post changes directly to Assembla (!), then refresh
    def __setitem__(self, key, item):
        if key not in self:
            raise NotImplementedError
        self.PUT(
            url  = self.get_set_url(key),
            body = etree.tostring(self.fromtuple(item))
        )
        self.refresh()

    def __delitem__(self, key):
        if key not in self:
            raise KeyError
        self.DELETE(url = self.get_del_url(key))
        self.refresh()

    def append(self, item):
        self.POST(
           url  = self.get_append_url(),
           body = etree.tostring(self.fromtuple(item)),
        )
        self.refresh()

    def fromtuple(self, t):
        xml = super(AssemblaIO, self).fromtuple(t)
        if self.skip_alerts:
            el = etree.SubElement(xml, 'skip-alerts')
            el.text = 'true'
        return xml


class UserIO(AssemblaIO):

    # XmlIO hints
    itemtag   = "user"
    key_field = "login"

    # NetIO url 
    @property
    def url(self):
        return super(UserIO, self).url + '/users'

class TicketIO(AssemblaIO):

    # XmlIO hints
    itemtag     = "ticket"
    field_names = "assigned-to-id completed-date component-id created-on description from-support id importance is-story milestone-id notification-list number priority reporter-id space-id status status-name story-importance summary updated-at working-hours working-hour estimate total-estimate invested-hours assigned-to reporter user-comment custom-fields"
    key_field   = "number"

    # Cache of CommentIO objects   
    comments = {}

    # NetIO url 
    @property
    def url(self):
        return super(TicketIO, self).url + '/tickets'

    # Use report 0 to ensure all tickets are returned by GET
    def GET(self, **kwargs):
        if 'url' not in kwargs:
            kwargs['url'] = self.url + '/report/0'
        return super(TicketIO, self).GET(**kwargs)

    def get_set_url(self, key):
        return self.url + '/' + str(key)

    def get_append_url(self):
        return self.url

    def totuple(self, xml):
        t = super(TicketIO, self).totuple(xml)
        cfxmls = xml.find('custom-fields')
        if cfxmls is None:
            return t
        else:
            cfields = {cfxml.get('name'): cfxml.text for cfxml in cfxmls}
            return t._replace(customfields = cfields)

    def fromtuple(self, t):
        cfields    = t.customfields
        reporterid = t.reporterid
        nosave = {field: None for field in ('workinghour', 'statusname', 'id', 'reporterid', 'fromsupport', 'investedhours', 'customfields')}
        t = t._replace(**nosave)
        xml = super(TicketIO, self).fromtuple(t)
        if cfields is not None and len(cfields) > 0:
            cfxmls = etree.SubElement(xml, 'custom-fields')
            for name, value in cfields.items():
                cfxml = etree.SubElement(cfxmls, name.replace(' ', '_'))
                cfxml.text = value
        if reporterid is not None:
            axml = etree.SubElement(xml, 'acts-as-user-id')
            axml.text = reporterid
        return xml

    def get_comments(self, tnum):
        if tnum not in self.comments:
            self.comments[tnum] = CommentIO(space = self.space, username = self.username,
                                            password = self.password, ticket = tnum)
        return self.comments[tnum]

class CommentIO(AssemblaIO):
    # XmlIO hints
    itemtag = "comment"
    field_names = "comment rendered created-on updated-at ticket-id user-id ticket-changes user"
    
    # NetIO url (read-only)
    @property
    def url(self):
        return super(CommentIO, self).url + '/tickets/' + self.ticket + '/comments'

    # Post new comments directly to Assembla (!)
    # Note: comments are sent to the ticket URL as ticket updates - i.e. not POSTed to /comments
    def append(self, item):
        ticket  = etree.Element('ticket');
        comment = etree.SubElement(ticket, 'user-comment')
        comment.text = unicode(item.comment)
        if item.createdon is not None:
            createdon = etree.SubElement(ticket, 'updated-at')
            createdon.text = unicode(item.createdon)
        if item.userid is not None:
            axml = etree.SubElement(ticket, 'acts-as-user-id')
            axml.text = item.userid
            
        if self.skip_alerts:
            el = etree.SubElement(ticket, 'skip-alerts')
            el.text = 'true'

        url = super(CommentIO, self).url + '/tickets/' + self.ticket
        self.PUT(
           url  = url,
           body = etree.tostring(ticket),
        )
        self.refresh()

class MilestoneIO(AssemblaIO):
    itemtag = "milestone"
    key_field = "title"
    @property
    def url(self):
        return super(MilestoneIO, self).url + '/milestones'

    def get_set_url(self, key):
        return self.url + '/' + str(self[key].id)

    def get_append_url(self):
        return self.url

class ComponentIO(AssemblaIO):
    itemtag = "component"
    key_field = "name"
    field_names = "id name"

    @property
    def url(self):
        return super(ComponentIO, self).url + '/tickets/components'

    def get_set_url(self, key):
        raise NotImplementedError

    def get_del_url(self, key):
        return super(ComponentIO, self).url + '/tickets/%s/remove_component' % self[key].id

    def get_append_url(self):
        return super(ComponentIO, self).url + '/tickets/create_component'

    def fromtuple(self, t):
        xml = etree.Element('component_name')
        xml.text = t.name
        return xml
