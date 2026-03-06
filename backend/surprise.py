class Surprise(dict):
	class Link(dict):
		def __init__(self, href: str, src: str):
			super().__init__(href=href, src=src)

	def __init__(self, name: str, description: str, photos: list[str], links: list[Link]):
		super().__init__(name=name, description=description, photos=photos, links=links)