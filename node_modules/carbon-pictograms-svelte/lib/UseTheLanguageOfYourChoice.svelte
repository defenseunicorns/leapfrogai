<script>
  /**
   * Specify the pictogram title.
   * @type {string}
   */
  export let title = undefined;

  $: labelled =  $$props["aria-label"] || $$props["aria-labelledby"] || $$props["title"];
  $: attributes = {
    "aria-hidden": labelled ? undefined : true,
    role: labelled ? "img" : undefined,
    focusable: Number($$props["tabindex"]) === 0  ? true : undefined,
  };
</script>

<svg
  preserveAspectRatio="xMidYMid meet"
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 32 32"
  width="64"
  height="64"
  fill="currentColor"
  {title}
  {...attributes}
  {...$$restProps}>
  <path d="M16,31.36	C7.53,31.36,0.64,24.47,0.64,16S7.53,0.64,16,0.64S31.36,7.53,31.36,16S24.47,31.36,16,31.36z M16.36,8.36v22.276	c2.864-0.069,5.527-0.966,7.758-2.458c-2.74-1.367-4.479-4.119-4.479-7.178V8.36H16.36z M2.654,22.018	c2.253,4.977,7.21,8.479,12.986,8.618V17.36H5.372L2.654,22.018z M20.36,8.36V21c0,2.912,1.732,5.519,4.433,6.698	C28.342,25.024,30.64,20.775,30.64,16c0-2.797-0.788-5.415-2.155-7.64H26.36V20h-0.72V8.36H20.36z M15.64,1.364	C7.733,1.556,1.36,8.048,1.36,16c0,1.824,0.335,3.571,0.948,5.184l8.381-14.365c0.065-0.112,0.205-0.152,0.315-0.178	c0.129,0.001,0.248,0.072,0.311,0.185l4.325,7.786C15.64,14.612,15.64,1.364,15.64,1.364z M5.792,16.64h9.848v-0.547l-4.648-8.366	L5.792,16.64z M16.36,7.64h11.653c-2.584-3.702-6.834-6.159-11.653-6.276V7.64z"></path>
</svg>