<script>
    async function logout() {
        let response = await fetch("http://localhost:8080/api/logout", {method: "GET"})
        response = await response
        if (response.status === 304 || response.status === 301 || response.status === 200) {
            window.location.assign(response.url)
        }
    }
</script>
{logout()}