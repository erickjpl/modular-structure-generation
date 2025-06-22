class QueryNotRegisteredError(Exception):
  def __init__(self, query):
    query_name = query.__class__.__name__ if hasattr(query, "__class__") else str(type(query))
    super().__init__(f"The query <{query_name}> hasn't a query handler associated")
