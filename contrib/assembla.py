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

    # NetIO url 
    @property
    def url(self):
        return "https://www.assembla.com/spaces/" + self.space

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
    field_names = "assigned-to-id completed-date component-id created-on description from-support id importance is-story milestone-id notification-list number priority reporter-id space-id status status-name story-importance summary updated-at working-hours working-hour estimate total-estimate invested-hours assigned-to reporter user-comment"
    key_field   = "number"

    # Cache of CommentIO objects   
    comments = {}

    # NetIO url 
    @property
    def url(self):
        return super(TicketIO, self).url + '/tickets'

    # Post ticket changes directly to Assembla (!)
    def __setitem__(self, key, item):
        if key not in self:
            raise NotImplementedError

        url = self.url + '/' + key
        self.PUT(
            url  = url,
            body = etree.tostring(self.fromtuple(item))
        )
        self.refresh()

    # Post ticket deletions directly to Assembla (!)
    def __delitem__(self, key):
        if key not in self:
            raise NotImplementedError
        url = self.url + '/' + str(key)
        self.DELETE(url = url)

    # Post new tickets directly to Assembla (!)
    def append(self, item):
        self.POST(
           body = etree.tostring(self.fromtuple(item)),
        )
        self.refresh()

    def fromtuple(self, t):
        nosave = {field: None for field in ('workinghour', 'statusname', 'id', 'reporterid', 'fromsupport', 'investedhours')}
        t = t._replace(**nosave)
        return super(TicketIO, self).fromtuple(t)

    def get_comments(self, tnum):
        if tnum not in self.comments:
            self.comments[tnum] = CommentIO(space = self.space, username = self.username,
                                            password = self.password, ticket = tnum)
        return self.comments[tnum]

class CommentIO(AssemblaIO):
    # XmlIO hints
    itemtag = "comment"
    
    # Ticket id
    ticket  = None

    # NetIO url (read-only)
    @property
    def url(self):
        return super(CommentIO, self).url + '/tickets/' + self.ticket + '/comments'

    # Post new comments directly to Assembla (!)
    # Note: comments are sent to the ticket URL as ticket updates - i.e. not POSTed to /comments
    def append(self, item):
        ticket  = etree.Element('ticket');
        comment = etree.SubElement(ticket, 'user-comment')
        comment.text = item.comment

        url = super(CommentIO, self).url + '/tickets/' + self.ticket
        self.PUT(
           url  = url,
           body = etree.tostring(ticket),
        )
        self.refresh()

