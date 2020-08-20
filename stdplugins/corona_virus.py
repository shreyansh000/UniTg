import asyncio
import aiohttp
from uniborg.util import admin_cmd

class AioHttp:
    @staticmethod
    async def get_json(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.json()

    @staticmethod
    async def get_text(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.text()

    @staticmethod
    async def get_raw(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.read()
                
@borg.on(admin_cmd(pattern="coronavirus (.*)", allow_sudo=True))
async def _(event):
    args = event.pattern_match.group(1)
    if not args:
        try:
            r = await AioHttp().get_json("https://corona.lmao.ninja/v2/all")
            reply_text = f"""**Global Cases 🦠:**
 - **Cases:** `{r['cases']:,}`
 - **Cases Today:** `{r['todayCases']:,}`
 - **Deaths:** `{r['deaths']:,}`
 - **Deaths Today:** `{r['todayDeaths']:,}`
 - **Recovered:** `{r['recovered']:,}`
 - **Active:** `{r['active']:,}`
 - **Critical:** `{r['critical']:,}`
 - **Cases/Mil:** `{r['casesPerOneMillion']}`
 - **Deaths/Mil:** `{r['deathsPerOneMillion']}``
"""
            await event.edit(f"{reply_text}")
            return
        except Exception as e:
            await event.edit("`The corona API could not be reached`")
            print(e)
            await asyncio.sleep(3)
            await message.delete()
            return
    country = args
    r = await AioHttp().get_json(f"https://corona.lmao.ninja/v2/countries/{country}")
    if "cases" not in r:
        await event.edit("```The country could not be found!```")
        await asyncio.sleep(3)
        await message.delete()
    else:
        try:
            reply_text = f"""**Cases for {r['country']} 🦠:**
 - **Cases:** `{r['cases']:,}`
 - **Cases Today:** `{r['todayCases']:,}`
 - **Deaths:** `{r['deaths']:,}`
 - **Deaths Today:** `{r['todayDeaths']:,}`
 - **Recovered:** `{r['recovered']:,}`
 - **Active:** `{r['active']:,}`
 - **Critical:** `{r['critical']:,}`
 - **Cases/Mil:** `{r['casesPerOneMillion']}`
 - **Deaths/Mil:** `{r['deathsPerOneMillion']}`
"""
            await event.edit(f"{reply_text}")
        except Exception as e:
            await event.edit("`The corona API could not be reached`")
            print(e)
            await asyncio.sleep(3)
            await message.delete()
