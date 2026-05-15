from typing import Annotated

from dagger import dag, function, object_type, check
import dagger

Source = Annotated[dagger.Directory, dagger.DefaultPath("/")]

@object_type
class CacheTest:
    @check
    @function
    async def foo(self):
        await dag.gingerbread().do_something()
        
    @check
    @function
    async def bar(self):
        await dag.gingerbread().do_something()                        