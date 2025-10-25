import math

class PaginateReturn:
    
    def __init__(self, items : list=[], page : int = 1, per_page: int=10, total: int=0) :
        self.items = items
        self.page = page
        self.per_page = per_page
        self.total = total
        pass
    
    def getPages(self) :
        total = self.total
        return math.ceil(total/self.per_page)
         
    
    
    def to_dict(self) :
        total = self.total
        pages = math.ceil(total/self.per_page)
        has_next = pages > self.page
        has_prev = self.page > 1

        return {
            "data": self.items,
            "pagination": {
                "total": total,
                "pages":pages,
                "has_prev":has_prev,
                "has_next":has_next,
                "page": self.page,
                "per_page": self.per_page
                
            }
        } 
                