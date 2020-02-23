from application.core.route.container import route_container
from application.views import IndexView

route_container.view("/index", IndexView)
route_container.redirect("/", "/index")
