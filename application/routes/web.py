from application.controller import IndexController, BBSController
from application.henavel.controller.routing.container import route_container

route_container.redirect("/", "/index")
route_container.controller("/index", IndexController)
route_container.controller("/bbs", BBSController)
