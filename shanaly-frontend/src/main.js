import App from './App.svelte'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'
import "bootstrap-icons/font/bootstrap-icons.css"
import './style.scss'

const app = new App({
  target: document.getElementById('app'),
})

export default app
