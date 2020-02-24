from application.controller.controllers import IndexController, BBSController
from application.henavel.controller.routing.route_manager import route_manager

route_manager.redirect("/", "/index")
route_manager.controller("/index", IndexController)
route_manager.controller("/bbs", BBSController)
