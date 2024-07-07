<script>
  import Router from 'svelte-spa-router'
  import Navigation from './components/Navigation.svelte'
  import Home from "./routes/Home.svelte"
  import Create from './routes/Create.svelte'
  import Search from "./routes/Search.svelte"
  import Profile from './routes/Profile.svelte'
  import TagSearch from './routes/TagSearch.svelte'
  import UserLogin from './routes/UserLogin.svelte'
  import SearchGeneral from './components/SearchGeneral.svelte'
  import UserSetting from './routes/UserSetting.svelte'
  
  const routes = {
    "/": Home,
    "/create": Create,
    "/search": Search,
    "/search/:tag": SearchGeneral,
    "/profile/:username": Profile,
    "/tag/:tag": TagSearch,
    "/user-login": UserLogin,
    "/user-setting": UserSetting,
  }
</script>

<Navigation/>

<Router {routes}/>