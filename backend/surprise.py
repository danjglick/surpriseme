class _Link(dict):
	def __init__(self, href, src):
		super().__init__(href=href, src=src)

class Surprise(dict):
	def __init__(self, name, description, photos, links: [_Link]):
		super().__init__(name=name, description=description, photos=photos, links=links)
