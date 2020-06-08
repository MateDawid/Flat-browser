class Offer:
  def __init__(self,page,title,price,area,URL):
    self.page = page
    self.title = title
    self.price = price
    self.area = area
    self.URL = URL
  def paramethers_list(self):
    return [self.page,self.title,self.price,self.area,self.URL]
