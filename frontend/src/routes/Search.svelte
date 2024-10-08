<script lang="ts">
  import { Button, Dropzone, Gallery, Label, P, Range, Select, Spinner } from "flowbite-svelte";
  import { getCollections, similaritySearch } from "../utils/backend";
  import ResultGallery from "../components/ResultGallery.svelte";
  import CollectionSelector from "../components/CollectionSelector.svelte";

  function handleChange(event) {
    query = [];
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = (e) => {
      query.push({ src: e.target.result });
      query = query;
    };
    reader.readAsDataURL(file);
  }

  function dropHandle(event) {
    event.preventDefault();
    const file = event.dataTransfer.items[0];
    if(file.kind === "file") {
      query = [];
      const reader = new FileReader();
      reader.onload = (e) => {
        query.push({ src: e.target.result });
        query = query;
      };
      reader.readAsDataURL(file.getAsFile());
    }
  }

  async function similaritySearchCall() {
    ongoing_query = true;
    result_images = await similaritySearch(collection_selection, query[0].src, number_of_results, similarity_threshold);
    ongoing_query = false;
  }

  // The state of the search site
  let collection_selection;
  let number_of_results = 5;
  let query = [];
  let ongoing_query = false;
  let result_images = [];
  let similarity_threshold = 50;
</script>

<div class="flex flex-col md:flex-row w-full mt-8">
  <div class="md:flex-shrink-0 md:w-1/4 w-full min-w-[300px] m-4">
    {#await getCollections()}
      <Label>
        Loading datasets...
      </Label>
    {:then options}
      <CollectionSelector data={options} bind:collection_selection={collection_selection}/>
    {/await}
    <Label class="pt-2">
      Number of results to show:
      <Select class="mt-2 p-4" items={[{"value": 5, "name": "5"}, {"value": 10, "name": "10"}, {"value": 20, "name": "20"}, {"value": 50, "name": "50"}, {"value": 100, "name": "100"}]} bind:value={number_of_results} />
    </Label>
    <Label class="pt-2">Similarity Threshold: {similarity_threshold}%
      <Range class="mt-2" min="0" max="100" step="0.01" bind:value={similarity_threshold} />
    </Label>
    <Button class="mt-4 w-full" color="blue" disabled="{ongoing_query}" on:click={similaritySearchCall}>
      Start Search {#if ongoing_query} <Spinner size="4" color="white"/> {/if}
    </Button>
    <!-- https://flowbite-svelte.com/docs/forms/file-input -->
    <Dropzone
      id="dropzone"
      on:change={handleChange}
      on:drop={dropHandle}
      on:dragover={(event) => { event.preventDefault(); }}
      class="w-full mt-4"
      >
      <p class="mb-2 text-sm text-gray-500 dark:text-gray-400"><span class="font-semibold">Click to upload</span> or drag and drop</p>
      <p class="text-xs text-gray-500 dark:text-gray-400">PNG, JPG or GIF</p>
    </Dropzone>
    <Gallery items={query} class="mt-4 w-full" />
  </div>
  <div class="md:flex-grow m-4 w-full min-w-[500px]">
    <Label>Similarity Search Results</Label>
    {#if ongoing_query}
      <div class="easydb-waiting flex justify-center">
        <P class="pt-24">
          <Spinner class="h-48 w-48"/>
        </P>
      </div>
    {:else}
      <ResultGallery class="h-full gap-4 grid-cols-3 mt-2 rounded-lg" items={result_images} />
    {/if}
  </div>
</div>
