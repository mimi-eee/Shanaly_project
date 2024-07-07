<script>
    import { link, push } from "svelte-spa-router";
    import { is_login, access_token, userid, username, email } from "../lib/store";
    import logo from "../lib/images/shanaly_logo.svg";
    import Wiki from "./Wiki.svelte";

    // if scrolling happens,
    // then give a change (scroll effect)
    // to the div component with ID mynav
    function userScroll() {
        const navbar = document.querySelector("[id='mynav']");

        window.addEventListener("scroll", () => {
            if (window.scrollY > 5) {
                navbar.classList.add("bg-white");
                navbar.classList.add("sticky-top");
            } else {
                navbar.classList.remove("bg-white");
                navbar.classList.remove("sticky-top");
            }
        })
    }
    document.addEventListener("DOMContentLoaded", userScroll);


    // If clicking any button in the hidden menu on the hamburger button, then close the modal
    function closeMenuModal() {
        // You need to set the proper id in the modal button!
        document.querySelector("[id='hidden-menu-button']").click();
    }

    function logout() {
        $is_login = false;
        $access_token = "";
        $userid = 0;
        $username = "";
        $email = "";
        push("/user-login");
        // Close the hamburger menu modal
        document.getElementById("hidden-menu-button").click();
    }

    function goToUserSetting() {
        // You need to set the proper id in the modal button!
        document.querySelector("[id='hidden-menu-button']").click();
        push("/user-setting");
    }

    function goToAdminShanaly() {
        // You need to set the proper id in the modal button!
        document.querySelector("[id='hidden-menu-button']").click();
        push("/admin-shanaly");
    }

</script>

<!-- Brand Name and Menu Button -->
<div class="container-sm" id="mynav">
    <div class="container my-2">
        <div class="row">
            <div class="col-7 px-0">
                <!-- Brand for Home Button -->
                <a use:link href="/" style="text-decoration: none;">
                    <h2 class="p-0 m-0">
                        <img src={logo} alt="Shanaly" style="width: 42px; height: 42px;"> Shanaly
                    </h2>
                </a>
            </div>
            <div class="col-5 px-0 d-flex justify-content-end gap-2">
                
                {#if $is_login === true}
                <!-- Wiki Button opens a offcanvs modal on the right side -->
                    <button
                    class="btn btn-outline-primary border-0"
                    type="button"
                    data-bs-toggle="offcanvas"
                    data-bs-target="#offcanvasRight"
                    aria-controls="offcanvasRight"
                    style="font-size: 13px;"
                >
                    <i class="bi bi-book"></i> 用語検索
                </button>
                {/if}

                <!-- Hamburger Button -->
                <button
                    class="btn btn-primary btn-lg btn-link p-0"
                    type="button"
                    id="main-hamburger"
                    data-bs-toggle="modal"
                    data-bs-target="#menuModal">
                    <i class="bi bi-list text-dark h2 fw-bold"></i>
                </button>
            </div>
        </div>
    </div>
</div>

<!-- Wiki Search Offcanvas -->
<div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">
    <div class="offcanvas-header">
        <h5 class="offcanvas-title" id="offcanvasRightLabel"><i class="bi bi-book"></i>   用語検索</h5>
        <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body">
        <!-- Wiki Component: Wiki.svelte -->
        <Wiki/>
    </div>
</div>

<!-- Modal for the Hidden Menu -->
<div class="modal fade" id="menuModal" tabindex="-1" aria-labelledby="menuModalLabel" aria-hidden="true">
    <div class="modal-dialog">
    <div class="modal-content">
        <div class="modal-header">
            <h1 class="modal-title fs-5" id="menuModalLabel">メニュー</h1>
            <!-- The next button has its own id! -->
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" id="hidden-menu-button"></button>
        </div>
        <div class="modal-body">

            <div class="btn-group-vertical d-flex gap-2" role="group" aria-label="Vertical button group">
                <!-- Logout Button -->
                {#if $is_login === true}
                    <button
                    type="button"
                    class="btn btn-outline-primary"
                    on:click={logout}>
                    <i class="bi bi-door-closed"></i> ログアウト
                    </button>
                    <button type="button" class="btn btn-outline-primary" on:click={goToUserSetting}><i class="bi bi-gear"></i> アカウント設定</button>
                {/if}
                <a class="btn btn-outline-primary" href="https://shanaly.net/" target="_blank"><i class="bi bi-stars"></i> サービスについて</a>
            </div>

        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-outline-primary" data-bs-dismiss="modal">閉じる</button>
        </div>
    </div>
    </div>
</div>


<style>

.container-sm {
    max-width: 576px;
}

#main-hamburger:hover {
    background-color:#fff!important;
    color:#000!important;
}

</style>