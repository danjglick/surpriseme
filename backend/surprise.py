class Surprise(dict):
	def __init__(self, name, description, photo, links):
		super().__init__(
			name=name,  
			description=description, 
			photo=photo, 
			links=links
		)
