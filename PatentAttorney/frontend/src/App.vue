<template>
  <v-app id = "app">
    <v-app-bar app color="indigo" dark >
      <v-toolbar-title>
        <router-link to="/">
          <v-icon>home</v-icon>
        </router-link>
        ImagePredict Service
      </v-toolbar-title>
    </v-app-bar>

    <v-content>
      <v-container>

        <router-view/>

      </v-container>
    </v-content>
    <v-footer color="indigo" app >
      <span class="white--text">&copy; 2019 KWU</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
    props: {
      source: String,
    },
    data: () => ({
      drawer: null,
    }),
  }
</script>

<style>

</style>
