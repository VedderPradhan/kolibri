<template>

  <div>

    <h3>{{ coreString('searchLabel') }}</h3>

    <SearchBox
      ref="searchBox"
      :filters="true"
    />

    <p v-if="!searchTerm">
      {{ $tr('noSearch') }}
    </p>

    <template v-else>
      <h1 class="search-results">
        {{ resultsMsg }}
      </h1>

      <ContentCardGroupGrid
        :genContentLink="genContentLink"
        :contents="contents"
      />

      <KButton
        v-if="contents.length < total_results && !loading"
        :text="coreString('viewMoreAction')"
        @click="loadMore"
      />
      <KCircularLoader
        v-else-if="contents.length < total_results && loading"
        :delay="false"
      />

    </template>
  </div>

</template>


<script>

  import { mapState } from 'vuex';
  import { ContentNodeKinds } from 'kolibri.coreVue.vuex.constants';
  import commonCoreStrings from 'kolibri.coreVue.mixins.commonCoreStrings';
  import { PageNames } from '../constants';
  import ContentCardGroupGrid from './ContentCardGroupGrid';
  import SearchBox from './SearchBox';

  export default {
    name: 'SearchPage',
    metaInfo() {
      return {
        title: this.coreString('searchLabel'),
      };
    },
    components: {
      ContentCardGroupGrid,
      SearchBox,
    },
    mixins: [commonCoreStrings],
    data() {
      return {
        loading: false,
      };
    },
    computed: {
      ...mapState('search', ['contents', 'searchTerm', 'total_results']),
      noResults() {
        return this.contents.length === 0;
      },
      resultsMsg() {
        if (this.noResults) {
          return this.$tr('noResultsMsg', { searchTerm: this.searchTerm });
        } else {
          return this.$tr('showingResultsFor', {
            searchTerm: this.searchTerm,
            totalResults: this.total_results,
          });
        }
      },
    },
    beforeDestroy() {
      // TODO do this clean up in a beforeRouteLeave once SearchPage is rendered in router-link
      this.$store.commit('search/RESET_STATE');
    },
    mounted() {
      // TODO when beforeRouteEnter is available, focus on filter or text input depending on what
      // was changed (e.g. if type filter was changed, focus on it after refresh)
      const inputRef = this.$refs.searchBox.$refs.searchInput;
      if (inputRef) {
        inputRef.focus();
        // If there are no results, then highlight the term, so user can try something else
        if (this.noResults) {
          inputRef.select();
        }
      }
    },
    methods: {
      genContentLink(contentId, contentKind) {
        const params = { id: contentId };
        if (contentKind === ContentNodeKinds.TOPIC || contentKind === ContentNodeKinds.CHANNEL) {
          return this.$router.getRoute(PageNames.TOPICS_TOPIC, params);
        }
        return this.$router.getRoute(PageNames.TOPICS_CONTENT, params, this.$route.query);
      },
      loadMore() {
        if (!this.loading) {
          this.loading = true;
          this.$store.dispatch('search/loadMore').then(() => {
            this.loading = false;
          });
        }
      },
    },
    $trs: {
      noSearch: 'Search by typing in the box above',
      showingResultsFor:
        "{totalResults, plural, one {{totalResults} result} other {{totalResults} results}} for '{searchTerm}'",
      noResultsMsg: "No results for '{searchTerm}'",
    },
  };

</script>


<style lang="scss" scoped>

  .search-results {
    margin-top: 32px;
  }

  .search-channel {
    font-size: smaller;
  }

</style>
