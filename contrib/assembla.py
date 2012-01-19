from wq.io import XmlIO, NetIO
from lxml import etree

# AssemblaIO
# a python implementation of
# http://www.assembla.com/spaces/breakoutdocs/wiki/Assembla_REST_API

class AssemblaIO(NetIO, XmlIO):
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
    itemtag = "user"
    itemkey = "login"

    # NetIO url 
    @property
    def url(self):
        return super(UserIO, self).url + '/users'

class TicketIO(AssemblaIO):

    # XmlIO hints
    itemtag  = "ticket"
    itemkey  = "number"

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
            body = etree.tostring(self.toxml(item))
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
           body = etree.tostring(self.toxml(item)),
        )
        self.refresh()

    # Include comments accessor in ticket
    def todict(self, el):
        ticket = super(TicketIO, self).todict(el)
        tnum   = ticket[self.itemkey]

        # Lazy load when ticket is requested
        if tnum not in self.comments:
            self.comments[tnum] = CommentIO(space = self.space, username = self.username,
                                            password = self.password, ticket = tnum)

        ticket['comments'] = self.comments[tnum]

        return ticket

    # Remove un-serializable comments accessor
    def toxml(self, ticket):
        if 'comments' in ticket:
            del ticket['comments']
        return super(TicketIO, self).toxml(ticket)

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
        comment.text = item['comment']

        url = super(CommentIO, self).url + '/tickets/' + self.ticket
        self.PUT(
           url  = url,
           body = etree.tostring(ticket),
        )
        self.refresh()

