import React from "react"
import ReactDOM from "react-dom"
import "./index.css"
import * as serviceWorker from "./serviceWorker"
import "bootstrap/dist/css/bootstrap.css"
import FrontEnd from "./components/frontEnd"

ReactDOM.render(<FrontEnd />, document.getElementById("root"))
serviceWorker.register()
