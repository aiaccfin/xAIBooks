import time, streamlit as st

def time_it(label="Running time"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            st.text(f"{label}耗时： {func.__name__}: {end_time - start_time:.6f} seconds")
            return result
        return wrapper
    return decorator
