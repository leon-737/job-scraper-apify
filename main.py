import asyncio
from apify import Actor
import requests
from bs4 import BeautifulSoup

async def main():
    async with Actor:
        # Obtenemos los parámetros de entrada del usuario
        actor_input = await Actor.get_input() or {}
        search_keyword = actor_input.get("keyword", "python").lower()
        
        Actor.log.info(f"Buscando ofertas de empleo para la palabra clave: '{search_keyword}'")

        # Usamos el feed RSS oficial de agregadores (ultra rápido, sin bloqueos de navegador ni GPU)
        rss_url = "https://weworkremotely.com/remote-jobs.rss"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        scraped_jobs = []

        try:
            response = requests.get(rss_url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                # Parseamos el XML del feed usando BeautifulSoup con parser nativo XML
                soup = BeautifulSoup(response.content, "xml")
                items = soup.find_all("item")
                
                Actor.log.info(f"Total de ofertas analizadas en el feed: {len(items)}")

                for item in items:
                    title = item.title.text if item.title else ""
                    link = item.link.text if item.link else ""
                    pub_date = item.pubDate.text if item.pubDate else ""
                    description = item.description.text if item.description else ""

                    # Filtrado inteligente por la palabra clave solicitada
                    if search_keyword in title.lower() or search_keyword in description.lower():
                        scraped_jobs.append({
                            "title": title,
                            "url": link,
                            "published_date": pub_date,
                            "keyword_matched": search_keyword,
                            "platform": "We Work Remotely (RSS)"
                        })
            else:
                Actor.log.error(f"Error al conectar con el servidor: Código {response.status_code}")

        except Exception as e:
            Actor.log.error(f"Error durante la extracción: {str(e)}")

        Actor.log.info(f"Proceso finalizado. Se guardaron {len(scraped_jobs)} ofertas coincidentes.")

        # Guardamos los resultados estructurados en el Dataset de Apify
        if scraped_jobs:
            await Actor.push_data(scraped_jobs)
        else:
            Actor.log.info("No se encontraron ofertas que coincidan con la búsqueda.")

if __name__ == "__main__":
    asyncio.run(main())

