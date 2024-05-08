from functools import wraps
import time

#? cet = calculate_execution_time


def cet(func): 
  """
  A decorator that measures the execution time of a function.

  Args:
    func: The function to be decorated.

  Returns:
    The decorated function.

  """
  @wraps(func)
  def wrapper(*args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time of {func.__name__}: {execution_time:.3f} seconds")
    return result
  return wrapper