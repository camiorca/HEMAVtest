# HEMAV Test

Dado que el servicio de la NASA no está en funcionamiento, recurrí a Landsatxplore, servicio que ofrece una integración
directa al servicio de USGS. Se usó el repositorio específico landsat_tm_c2_l1, teniendo en cuenta que existían
restricciones de permisos con una cuenta nueva.

URL de la librería: https://pypi.org/project/landsatxplorer
Landsat repo: https://landsat.usgs.gov

## Infraestructura planeada

Teniendo en cuenta la necesidad de ejecución diaria, se plantea una configuración con AWS Lambda, con un trigger "on a 
schedule", haciendo llamado de los servicios de la aplicación.

Se usó Docker como herramienta de contenerización, para usarlo por facilidad para configurar Lambda. Los llamados serían
todos los días a media noche, para así facilitar la ejecución.