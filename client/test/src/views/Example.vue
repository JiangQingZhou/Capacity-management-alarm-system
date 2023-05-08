<template>
    <div class="common-layout">
        <el-container class="container">
            <el-aside class="aside">
                <el-menu :default-active="activeIndex" router unique-opened>
                    <el-sub-menu index="/">
                        <template #title>
                            <el-icon><HomeFilled /></el-icon>
                            容量预测告警系统
                        </template>
                        <el-menu-item index="/one"><el-icon><InfoFilled /></el-icon>第一题</el-menu-item>
                        <el-menu-item index="/two"><el-icon><WarningFilled /></el-icon>第二题</el-menu-item>
                    </el-sub-menu>
                </el-menu>
            </el-aside>

            <el-container>
                <el-main class="main">
                    <router-view v-slot="{ Component }">
                        <keep-alive>
                            <component :is="Component" />
                        </keep-alive>
                    </router-view>
                </el-main>
            </el-container>
        </el-container>
    </div>

</template>

<script>
    export default {
        data() {
            return {
                activeIndex: '/one',
            }
        },
        mounted() {
            this.activeIndex = this.$route.path
        },
        methods: {
        }
    }
</script>

<style scoped>
    .common-layout {
        width: 100%;
        height: 100%;
        margin: 0;
        padding: 0;
    }
    .container {
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        margin: 0;
        padding: 0;
        height: 100%;
        width: 100%;
    }

    .aside {
        background-color: rgba(245,245,245, 0.9);
        width: 200px;
        height: 100%;
    }

    .menu {
        background-color: transparent;
        /* border-right: none; */
        height: 100%;
    }

    .main {
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        margin: 0;
        padding: 0;
        height: 100%;
        width: 100%;
        position: relative;
        background-color: white;
    }
</style>