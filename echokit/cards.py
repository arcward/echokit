class SimpleCard:
    """Simple card, supporting only *title* and *content*"""

    def __init__(self, title=None, content=None):
        self.type = 'Simple'
        self.title = title
        self.content = content

    def _dict(self):
        return self.__dict__


class StandardCard:
    """Standard card, supporting title/text and a (small/large) image"""

    def __init__(self, title=None, text=None, small_image_url=None,
                 large_image_url=None):
        self.type = 'Standard'
        self.title = title
        self.text = text
        self.small_image_url = small_image_url
        self.large_image_url = large_image_url

    @property
    def image(self):
        """If any image URL is provided, return dict, otherwose None"""
        if not (self.small_image_url or self.large_image_url):
            return None
        img = {}
        if self.small_image_url:
            img['smallImageUrl'] = self.small_image_url
        if self.large_image_url:
            img['largeImageUrl'] = self.large_image_url
        return img

    def _dict(self):
        card_dict = {'type': self.type}
        if self.title:
            card_dict['title'] = self.title
        if self.text:
            card_dict['text'] = self.text
        if self.image:
            card_dict['image'] = self.image
        return card_dict


class LinkAccountCard:
    """LinkAccount card, supporting only *content*"""

    def __init__(self, content=None):
        self.type = 'LinkAccount'
        self.content = content

    def _dict(self):
        return self.__dict__
