<script lang="ts">
  import { FileOutline } from 'flowbite-svelte-icons';
  import { getFileType } from '$lib/utils/files.js';
  import {Card} from "flowbite-svelte";

  export let name: string;
  export let type: string;
</script>

<Card horizontal padding="xs" class="w-32">
  <div class="flex gap-2">
  <div class="flex items-center rounded-lg p-2 bg-gray-700">
  <FileOutline size="lg" color="white"/>
  </div>
  <div class="flex flex-col">
  <h5 class="text-sm font-bold text-gray-900 dark:text-white">
    {name}
  </h5>
  <p class="text-sm font-normal text-gray-700 dark:text-gray-400">
    {getFileType(type)}
  </p>
  </div>
  </div>
</Card>
