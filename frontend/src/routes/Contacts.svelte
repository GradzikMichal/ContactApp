<script>
    let contact_info = $state({
        id:0,
        name: "",
        surname: "",
        email: "",
        phone: "",
        city: "",
        status: "new",
        add_date: ""

    })
    let contact_statuses = $state([])
    let csrf = $state()
    let contacts = $state([])

    document.addEventListener("DOMContentLoaded", () => {
        const contact_form = document.getElementById("contactForm")
        contact_form.addEventListener("submit", handleContactSubmit)
        const edit_contact_form = document.getElementById("editContactForm")
        edit_contact_form.addEventListener("submit", handleContactEdit)
    })

    async function getContacts(){
        try{
            let response =  await fetch("http://localhost:8080/api/contacts/",
                {
                    method: "GET",
                }).then(response => response.json())
            csrf = response["csrf"]
            contact_statuses = response["contact_statuses"]
            contacts = JSON.parse(response["contacts"])
        }catch(err){
            document.getElementById("infoMessage").innerHTML = err;
            document.getElementById("infoModal").showModal();
        }
    }

    function openAddContactModal(){
        contact_info = {
            id:0,
            name: "",
            surname: "",
            email: "",
            phone: "",
            city: "",
            status: "new",
            add_date: ""

        }
        document.getElementById("contactModal").showModal();
    }

    function handleContactSubmit(e){
        e.preventDefault();
        sendData();
    }

    function handleContactEdit(e){
        e.preventDefault();
        editContact();
    }

    async function sendData(){
        document.getElementsByClassName("loading")[0].classList.remove("hidden")
        try {
            let response = await fetch("http://localhost:8080/api/contacts/",
                {
                    method: "POST",
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        "Mode": 'cors',
                        "Credentials": 'same-origin',
                        "Cookie": document.cookie,
                        "X-CSRFToken": csrf
                    },
                    body: JSON.stringify(contact_info),
                }).then(response => response.json())

                contacts = JSON.parse(response)

        }catch (err){
            document.getElementById("infoMessage").innerHTML = err
            console.log(err)
            document.getElementsByClassName("loading")[0].classList.add("hidden");
            document.getElementById("infoModal").showModal();
            return;
        }
        document.getElementsByClassName("loading")[0].classList.add("hidden");
        document.getElementById("contactModal").close();
        contact_info = {
            id:0,
            name: "",
            surname: "",
            email: "",
            phone: "",
            city: "",
            status: "new",
            add_date: ""
        };
        document.getElementById("infoMessage").innerHTML = "Contacts successfully added";
        document.getElementsByClassName("loading")[0].classList.add("hidden");
        document.getElementById("infoModal").showModal();
    }

    function openEditContactModal(contact_id){
        const contact_data =  contacts.find(contact => contact["pk"] === contact_id)['fields']
        contact_info = {...contact_data, city:contact_data.city.name, id: contact_id, status: contact_data.status.name}
        document.getElementById("contactModalEdit").showModal();
    }

    async function editContact() {
        document.getElementsByClassName("loading")[0].classList.remove("hidden")
        try {
            let response = await fetch("http://localhost:8080/api/contacts/"+contact_info.id+"/",
                {
                    method: "PUT",
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        "Mode": 'cors',
                        "Credentials": 'same-origin',
                        "Cookie": document.cookie,
                        "X-CSRFToken": csrf
                    },
                    body: JSON.stringify(contact_info),
                }).then(response => response.json())
            document.getElementById("infoMessage").innerHTML = response.message
            document.getElementById("infoModal").showModal();
        }catch (err){
            document.getElementById("infoMessage").innerHTML = err
            console.log(err)
            document.getElementsByClassName("loading")[0].classList.add("hidden");
            document.getElementById("infoModal").showModal();
            return;
        }
        let changedContact = contacts[contacts.findIndex(contact => contact["pk"] === contact_info.id)]
        changedContact["fields"].city.name = contact_info.city
        changedContact["fields"].status.name=contact_info.status
        contacts[contacts.findIndex(contact => contact["pk"] === contact_info.id)]["fields"] = {...contact_info, city: changedContact["fields"].city, status: changedContact["fields"].status}
        document.getElementsByClassName("loading")[0].classList.add("hidden");
        document.getElementById("contactModalEdit").close();
        contact_info = {
            id:0,
            name: "",
            surname: "",
            email: "",
            phone: "",
            city: "",
            status: "new",
            add_date: ""
        };
    }

    function openDeleteContactModal(contact_id){
        const contact_data =  contacts.find(contact => contact["pk"] === contact_id)['fields']
        contact_info = {...contact_data, city:contact_data.city.name, id: contact_id, status: contact_data.status.name}
        document.getElementById("contactModalDelete").showModal();
    }

    function closeDeleteModal(){
        document.getElementById("contactModalDelete").close();
    }

    async function deleteContact() {
        document.getElementsByClassName("loading")[0].classList.remove("hidden")
        try {
            let response = await fetch("http://localhost:8080/api/contacts/"+contact_info.id+"/",
                {
                    method: "DELETE",
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        "Mode": 'cors',
                        "Credentials": 'same-origin',
                        "Cookie": document.cookie,
                        "X-CSRFToken": csrf
                    },
                }).then(response => response.json())
            document.getElementById("infoMessage").innerHTML = response.message
            document.getElementById("infoModal").showModal();
        }catch (err){
            document.getElementById("infoMessage").innerHTML = err
            console.log(err)
            document.getElementsByClassName("loading")[0].classList.add("hidden");
            document.getElementById("infoModal").showModal();
            return;
        }
        document.getElementsByClassName("loading")[0].classList.add("hidden");
        document.getElementById("contactModalDelete").close();
        contacts.splice(contacts.findIndex(contact => contact["pk"] === contact_info.id),1)
        contact_info = {
            id:0,
            name: "",
            surname: "",
            email: "",
            phone: "",
            city: "",
            status: "new",
            add_date: ""
        };
    }

    function sortContactsBy(type, by) {
        contacts.sort((a, b) => (a['fields'][type]>b['fields'][type]) ? 1 * by : ((a['fields'][type]<b['fields'][type]) ? -1 * by : 0))
        contacts = contacts
    }
</script>

{#snippet contact(contact_info, contact_id)}
    <div class="card sm:w-100 xl:w-full bg-base-100 card-md shadow-sm">
        <div class="card-body">

            <div class="card-title flex justify-between">
                <div>
                    {contact_info.name} {contact_info.surname}
                </div>
                <div>
                    <button class="task-btn edit-btn" onclick={()=>openEditContactModal(contact_id)}>
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                        </svg>
                    </button>
                    <button class="task-btn delete-btn" onclick={()=>openDeleteContactModal(contact_id)}>
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="3 6 5 6 21 6"></polyline>
                            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                        </svg>
                    </button>
                </div>
            </div>
            <div class="card-action xl:w-fit xl:mx-auto">
                <div class="flex flex-row">
                    <div class="flex sm:flex-col sm:w-2/3 xl:flex-row xl:w-fit">
                        <div class="badge badge-soft badge-primary">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-telephone" viewBox="0 0 16 16">
                                <path d="M3.654 1.328a.678.678 0 0 0-1.015-.063L1.605 2.3c-.483.484-.661 1.169-.45 1.77a17.6 17.6 0 0 0 4.168 6.608 17.6 17.6 0 0 0 6.608 4.168c.601.211 1.286.033 1.77-.45l1.034-1.034a.678.678 0 0 0-.063-1.015l-2.307-1.794a.68.68 0 0 0-.58-.122l-2.19.547a1.75 1.75 0 0 1-1.657-.459L5.482 8.062a1.75 1.75 0 0 1-.46-1.657l.548-2.19a.68.68 0 0 0-.122-.58zM1.884.511a1.745 1.745 0 0 1 2.612.163L6.29 2.98c.329.423.445.974.315 1.494l-.547 2.19a.68.68 0 0 0 .178.643l2.457 2.457a.68.68 0 0 0 .644.178l2.189-.547a1.75 1.75 0 0 1 1.494.315l2.306 1.794c.829.645.905 1.87.163 2.611l-1.034 1.034c-.74.74-1.846 1.065-2.877.702a18.6 18.6 0 0 1-7.01-4.42 18.6 18.6 0 0 1-4.42-7.009c-.362-1.03-.037-2.137.703-2.877z"/>
                            </svg>
                            {contact_info.phone}
                        </div>
                        <div class="badge badge-soft badge-primary">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-envelope-open" viewBox="0 0 16 16">
                                <path d="M8.47 1.318a1 1 0 0 0-.94 0l-6 3.2A1 1 0 0 0 1 5.4v.817l5.75 3.45L8 8.917l1.25.75L15 6.217V5.4a1 1 0 0 0-.53-.882zM15 7.383l-4.778 2.867L15 13.117zm-.035 6.88L8 10.082l-6.965 4.18A1 1 0 0 0 2 15h12a1 1 0 0 0 .965-.738ZM1 13.116l4.778-2.867L1 7.383v5.734ZM7.059.435a2 2 0 0 1 1.882 0l6 3.2A2 2 0 0 1 16 5.4V14a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V5.4a2 2 0 0 1 1.059-1.765z"/>
                            </svg>
                            {contact_info.email}

                        </div>
                        <div class="badge badge-soft badge-primary">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-house" viewBox="0 0 16 16">
                                <path d="M8.707 1.5a1 1 0 0 0-1.414 0L.646 8.146a.5.5 0 0 0 .708.708L2 8.207V13.5A1.5 1.5 0 0 0 3.5 15h9a1.5 1.5 0 0 0 1.5-1.5V8.207l.646.647a.5.5 0 0 0 .708-.708L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293zM13 7.207V13.5a.5.5 0 0 1-.5.5h-9a.5.5 0 0 1-.5-.5V7.207l5-5z"/>
                            </svg>
                            {contact_info.city.name}
                        </div>
                        <div class="badge badge-soft badge-primary">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-info" viewBox="0 0 16 16">
                                <path d="m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0"/>
                            </svg>
                            {contact_info.status.name}
                        </div>
                    </div>
                    <div class="flex sm:flex-col sm:w-1/3 xl:flex-row xl:w-fit">
                        <div class="badge badge-soft badge-warning">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-thermometer-half" viewBox="0 0 16 16">
                                <path d="M9.5 12.5a1.5 1.5 0 1 1-2-1.415V6.5a.5.5 0 0 1 1 0v4.585a1.5 1.5 0 0 1 1 1.415"/>
                                <path d="M5.5 2.5a2.5 2.5 0 0 1 5 0v7.55a3.5 3.5 0 1 1-5 0zM8 1a1.5 1.5 0 0 0-1.5 1.5v7.987l-.167.15a2.5 2.5 0 1 0 3.333 0l-.166-.15V2.5A1.5 1.5 0 0 0 8 1"/>
                            </svg>
                            {contact_info.city.temperature} &deg;C
                        </div>
                        <div class="badge badge-soft badge-info">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-moisture" viewBox="0 0 16 16">
                                <path d="M13.5 0a.5.5 0 0 0 0 1H15v2.75h-.5a.5.5 0 0 0 0 1h.5V7.5h-1.5a.5.5 0 0 0 0 1H15v2.75h-.5a.5.5 0 0 0 0 1h.5V15h-1.5a.5.5 0 0 0 0 1h2a.5.5 0 0 0 .5-.5V.5a.5.5 0 0 0-.5-.5zM7 1.5l.364-.343a.5.5 0 0 0-.728 0l-.002.002-.006.007-.022.023-.08.088a29 29 0 0 0-1.274 1.517c-.769.983-1.714 2.325-2.385 3.727C2.368 7.564 2 8.682 2 9.733 2 12.614 4.212 15 7 15s5-2.386 5-5.267c0-1.05-.368-2.169-.867-3.212-.671-1.402-1.616-2.744-2.385-3.727a29 29 0 0 0-1.354-1.605l-.022-.023-.006-.007-.002-.001zm0 0-.364-.343zm-.016.766L7 2.247l.016.019c.24.274.572.667.944 1.144.611.781 1.32 1.776 1.901 2.827H4.14c.58-1.051 1.29-2.046 1.9-2.827.373-.477.706-.87.945-1.144zM3 9.733c0-.755.244-1.612.638-2.496h6.724c.395.884.638 1.741.638 2.496C11 12.117 9.182 14 7 14s-4-1.883-4-4.267"/>
                            </svg>
                            {contact_info.city.humidity} %
                        </div>
                        <div class="badge badge-soft badge-accent">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-wind" viewBox="0 0 16 16">
                                <path d="M12.5 2A2.5 2.5 0 0 0 10 4.5a.5.5 0 0 1-1 0A3.5 3.5 0 1 1 12.5 8H.5a.5.5 0 0 1 0-1h12a2.5 2.5 0 0 0 0-5m-7 1a1 1 0 0 0-1 1 .5.5 0 0 1-1 0 2 2 0 1 1 2 2h-5a.5.5 0 0 1 0-1h5a1 1 0 0 0 0-2M0 9.5A.5.5 0 0 1 .5 9h10.042a3 3 0 1 1-3 3 .5.5 0 0 1 1 0 2 2 0 1 0 2-2H.5a.5.5 0 0 1-.5-.5"/>
                            </svg>
                            {contact_info.city.wind_speed} km/h
                        </div>
                    </div>
                </div>
                <div>
                    <div class="badge badge-xs badge-outline badge-warn">
                        {contact_info.add_date.split(".")[0].split("T")[0]} {contact_info.add_date.split(".")[0].split("T")[1]}
                    </div>
                </div>

            </div>
        </div>
    </div>
{/snippet}

<div>
    <header class="header px-0 z-50">
        <div class="container">
            <div class="header-content flex items-center justify-end p-4">
                <div class="dropdown">
                    <div tabindex="0" role="button" class="btn btn-soft btn-info btn-ghost rounded-field">Sort by</div>
                    <ul class="menu dropdown-content bg-base-100 rounded-box z-1 w-52 p-2 shadow-sm">
                        <li >
                            <button onclick={()=>sortContactsBy('surname', 1)}>
                                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-sort-alpha-down" viewBox="0 0 16 16">
                                    <path fill-rule="evenodd" d="M10.082 5.629 9.664 7H8.598l1.789-5.332h1.234L13.402 7h-1.12l-.419-1.371zm1.57-.785L11 2.687h-.047l-.652 2.157z"/>
                                    <path d="M12.96 14H9.028v-.691l2.579-3.72v-.054H9.098v-.867h3.785v.691l-2.567 3.72v.054h2.645zM4.5 2.5a.5.5 0 0 0-1 0v9.793l-1.146-1.147a.5.5 0 0 0-.708.708l2 1.999.007.007a.497.497 0 0 0 .7-.006l2-2a.5.5 0 0 0-.707-.708L4.5 12.293z"/>
                                </svg>
                                Surname
                            </button>
                        </li>
                        <li>
                            <button onclick={()=>sortContactsBy("surname", -1)}>
                            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-sort-alpha-down-alt" viewBox="0 0 16 16">
                                <path d="M12.96 7H9.028v-.691l2.579-3.72v-.054H9.098v-.867h3.785v.691l-2.567 3.72v.054h2.645z"/>
                                <path fill-rule="evenodd" d="M10.082 12.629 9.664 14H8.598l1.789-5.332h1.234L13.402 14h-1.12l-.419-1.371zm1.57-.785L11 9.688h-.047l-.652 2.156z"/>
                                <path d="M4.5 2.5a.5.5 0 0 0-1 0v9.793l-1.146-1.147a.5.5 0 0 0-.708.708l2 1.999.007.007a.497.497 0 0 0 .7-.006l2-2a.5.5 0 0 0-.707-.708L4.5 12.293z"/>
                            </svg>
                            Surname
                        </button>
                        </li>
                        <li>
                            <button onclick={()=>sortContactsBy("add_date", 1)}>
                            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-sort-numeric-down" viewBox="0 0 16 16">
                                <path d="M12.438 1.668V7H11.39V2.684h-.051l-1.211.859v-.969l1.262-.906h1.046z"/>
                                <path fill-rule="evenodd" d="M11.36 14.098c-1.137 0-1.708-.657-1.762-1.278h1.004c.058.223.343.45.773.45.824 0 1.164-.829 1.133-1.856h-.059c-.148.39-.57.742-1.261.742-.91 0-1.72-.613-1.72-1.758 0-1.148.848-1.835 1.973-1.835 1.09 0 2.063.636 2.063 2.687 0 1.867-.723 2.848-2.145 2.848zm.062-2.735c.504 0 .933-.336.933-.972 0-.633-.398-1.008-.94-1.008-.52 0-.927.375-.927 1 0 .64.418.98.934.98"/>
                                <path d="M4.5 2.5a.5.5 0 0 0-1 0v9.793l-1.146-1.147a.5.5 0 0 0-.708.708l2 1.999.007.007a.497.497 0 0 0 .7-.006l2-2a.5.5 0 0 0-.707-.708L4.5 12.293z"/>
                            </svg>
                            Add date
                            </button>
                        </li>
                        <li>
                            <button onclick={()=>sortContactsBy("add_date", -1)}>
                                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-sort-numeric-down-alt" viewBox="0 0 16 16">
                                    <path fill-rule="evenodd" d="M11.36 7.098c-1.137 0-1.708-.657-1.762-1.278h1.004c.058.223.343.45.773.45.824 0 1.164-.829 1.133-1.856h-.059c-.148.39-.57.742-1.261.742-.91 0-1.72-.613-1.72-1.758 0-1.148.848-1.836 1.973-1.836 1.09 0 2.063.637 2.063 2.688 0 1.867-.723 2.848-2.145 2.848zm.062-2.735c.504 0 .933-.336.933-.972 0-.633-.398-1.008-.94-1.008-.52 0-.927.375-.927 1 0 .64.418.98.934.98"/>
                                    <path d="M12.438 8.668V14H11.39V9.684h-.051l-1.211.859v-.969l1.262-.906h1.046zM4.5 2.5a.5.5 0 0 0-1 0v9.793l-1.146-1.147a.5.5 0 0 0-.708.708l2 1.999.007.007a.497.497 0 0 0 .7-.006l2-2a.5.5 0 0 0-.707-.708L4.5 12.293z"/>
                                </svg>
                                Add date
                            </button>
                        </li>
                    </ul>
                </div>
                <button class="btn btn-info w-fit h-10" id="addContactBtn" onclick={()=> openAddContactModal()}>
                        <svg width="25" height="25" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="inline">
                            <line x1="12" y1="5" x2="12" y2="19"></line>
                            <line x1="5" y1="12" x2="19" y2="12"></line>
                        </svg>
                        Add Contact
                </button>
            </div>
        </div>
    </header>
    {#await getContacts() then _}
        <ul class="menu bg-base-200 xl:w-2/3 sm:w-108 p-4 mx-auto space-y-4">
            {#key contacts}
                {#each contacts as contact_info, _}
                    {@render contact(
                        contact_info["fields"], contact_info["pk"]
                    )}
                {/each}
            {/key}
        </ul>
    {/await}
</div>

<dialog class="modal" id="contactModal">
    <div class="modal-box modal-content">
        <div class="modal-header">
            <div class="modal-action">
                <form method="dialog">
                    <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
                </form>
            </div>
            <h3 class="modal-title" id="modalTitle">Add new contact</h3>
        </div>
        <form id="contactForm" action="javascript:void(0);" class="rounded-box p-4">
            {#key contact_info}
                <fieldset class="fieldset">
                    <label for="name">Name:</label>
                    <input type="text" id="name" name="name" class="input validator" placeholder="Contact name" required bind:value={contact_info.name}>
                    <p class="validator-hint hidden">Required</p>
                </fieldset>
                <fieldset class="fieldset">
                    <label for="surname">Surname:</label>
                    <input type="text" id="surname" name="surname" class="input validator" placeholder="Contact surname" required bind:value={contact_info.surname}>
                    <p class="validator-hint hidden">Required</p>
                </fieldset>
                <fieldset class="fieldset">
                    <label for="email">Email:</label>
                    <input type="email" id="email" name="email" class="input validator" placeholder="Contact email" required bind:value={contact_info.email}>
                    <p class="validator-hint hidden">Required</p>
                </fieldset>
                <fieldset class="fieldset">
                    <label for="number">Phone number:</label>
                    <input type="tel" id="number" name="number" class="input validator" placeholder="48123456789" pattern="[0-9]*" minlength="11" maxlength="11" required bind:value={contact_info.phone}>
                    <p class="validator-hint hidden">Required. Should have 11 numbers - 2 country code, 9 phone number!</p>
                </fieldset>
                <fieldset class="fieldset">
                    <label for="city">City:</label>
                    <input type="text" id="city" name="city" class="input validator" placeholder="City name" required  bind:value={contact_info.city}>
                    <p class="validator-hint hidden">Required</p>
                </fieldset>
                <fieldset class="fieldset">
                    <label for="status">Status:</label>
                    <select class="select">
                        {#each contact_statuses as status}
                            {#if contact_info.status === status.name}
                                <option selected>{status.name}</option>
                            {:else}
                                <option>{status.name}</option>
                            {/if}
                        {/each}
                    </select>
                    <p class="validator-hint hidden">Required</p>
                </fieldset>
                <div>
                    <button type="submit" class="btn btn-primary" id="saveContactBtn">
                        Save contact
                        <span class="loading loading-spinner loading-xs hidden"></span>
                    </button>
                </div>
            {/key}
        </form>
    </div>
</dialog>

<dialog class="modal" id="contactModalEdit">
    <div class="modal-box modal-content">
        <div class="modal-header">
            <div class="modal-action">
                <form method="dialog">
                    <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
                </form>
            </div>
            <h3 class="modal-title" id="modalTitle">Edit contact</h3>
        </div>
        <form id="editContactForm" action="javascript:void(0);" class="rounded-box p-4">
            {#key contact_info}
                <fieldset class="fieldset">
                    <label for="name">Name:</label>
                    <input type="text" id="name" name="name" class="input validator" placeholder="Contact name" required bind:value={contact_info.name}>
                    <p class="validator-hint hidden">Required</p>
                </fieldset>
                <fieldset class="fieldset">
                    <label for="surname">Surname:</label>
                    <input type="text" id="surname" name="surname" class="input validator" placeholder="Contact surname" required bind:value={contact_info.surname}>
                    <p class="validator-hint hidden">Required</p>
                </fieldset>
                <fieldset class="fieldset">
                    <label for="email">Email:</label>
                    <input type="email" id="email" name="email" class="input validator" placeholder="Contact email" required bind:value={contact_info.email}>
                    <p class="validator-hint hidden">Required</p>
                </fieldset>
                <fieldset class="fieldset">
                    <label for="number">Phone number:</label>
                    <input type="tel" id="number" name="number" class="input validator" placeholder="48123456789" pattern="[0-9]*" minlength="11" maxlength="11" required bind:value={contact_info.phone}>
                    <p class="validator-hint hidden">Required. Should have 11 numbers - 2 country code, 9 phone number!</p>
                </fieldset>
                <fieldset class="fieldset">
                    <label for="city">City:</label>
                    <input type="text" id="city" name="city" class="input validator" placeholder="City name" required  bind:value={contact_info.city}>
                    <p class="validator-hint hidden">Required</p>
                </fieldset>
                <fieldset class="fieldset">
                    <label for="status">Status:</label>
                    <select bind:value={contact_info.status} class="select">
                        {#each contact_statuses as status}
                            {#if contact_info.status === status.name}
                                <option selected>{status.name}</option>
                            {:else}
                                <option>{status.name}</option>
                            {/if}
                        {/each}
                    </select>
                    <p class="validator-hint hidden">Required</p>
                </fieldset>
                <div>
                    <button type="submit" class="btn btn-primary" id="editContactBtn">
                        Save contact
                        <span class="loading loading-spinner loading-xs hidden"></span>
                    </button>
                </div>
            {/key}
        </form>
    </div>
</dialog>

<dialog class="modal" id="contactModalDelete">
    <div class="modal-box modal-content">
        <div class="modal-header">
            <div class="modal-action">
                <form method="dialog">
                    <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
                </form>
            </div>
            <h3 class="modal-title" id="modalTitle">Do you want to delete the contact?</h3>
        </div>
        <p class="py-4">Do you really want to delete the contact?</p>


        <button class="btn btn-success" onclick={()=>deleteContact()} >
            Delete contact
            <span class="loading loading-spinner loading-xs hidden"></span>
        </button>
        <button class="btn btn-error" onclick={()=>closeDeleteModal()} >
            Cancel
            <span class="loading loading-spinner loading-xs hidden"></span>
        </button>
    </div>
</dialog>

<dialog class="modal" id="infoModal">

    <div class="modal-box">
        <form method="dialog">
            <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
        </form>
        <h3 class="text-lg font-bold">Info!</h3>
        <p class="py-4" id="infoMessage">Info</p>
    </div>

</dialog>
