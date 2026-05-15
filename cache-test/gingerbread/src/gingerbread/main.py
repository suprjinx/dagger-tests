from typing import Annotated

from dagger import dag, function, object_type, check
import dagger

Source = Annotated[dagger.Directory, dagger.DefaultPath("/")]

script = """
n="$RANDOM"

echo "$(ls /gingerbread): $n" >> /cache/shared_file.txt
i=1
while [ $i -le 10 ]
do
  echo $n >> /cache/shared_file.txt
  sleep 0.1
  i=$((i + 1))
done
"""

@object_type
class Gingerbread:
    @check
    @function
    async def bar(self, src: Source):
        await self.do_something(src)

    @function
    async def do_something(self, src: Source) -> None:
        cache = dag.cache_volume("some_cache")
        await (dag.container().from_("alpine:latest").with_mounted_cache("/cache", cache)
               .with_mounted_directory("/gingerbread", src)
               .with_exec(["sh", "-c", script])).sync()

    @function
    async def read(self) -> str:
        cache = dag.cache_volume("some_cache")
        return await dag.container().from_("alpine:latest").with_mounted_cache("/cache", cache).with_exec(["cat", "/cache/shared_file.txt"]).stdout()        