<script setup>

import router from '../../router/index';

const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_role');
    router.push("/login");
};

</script>


<style>


.ExitButton{
    background-color: red;
    transition: 0.5s;
}


.ExitButton:hover{
    background-color: rgb(253, 169, 169);
}

</style>

<template>
    <div>
        <button @click="logout()" class="ExitButton">Exit</button>
    </div>
</template>


