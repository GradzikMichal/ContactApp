<script>
  import {Route, Router, Link} from "svelte5-router";
  import Login from "./routes/Login.svelte";
  import Logout from "./routes/Logout.svelte";
  import Contacts from "./routes/Contacts.svelte";
  let {url = ""} =$props();
</script>

<Router {url}>
    <div class="navbar bg-base-100 shadow-sm max-h-1/20">
        <div class="flex-none">
            <ul class="menu menu-horizontal px-1">
                <li>
                    <Link to="/contacts">
                        Contacts
                    </Link>
                </li>
                <li>
                    <Link to="/logout">
                        Logout
                    </Link>
                </li>
            </ul>
        </div>
    </div>
    <div class="max-h-19/20">
        <Route path="/login" replace component={Login}/>
        <Route path="/contacts" replace component={Contacts}/>
        <Route path="/logout" replace component={Logout}/>
    </div>

</Router>