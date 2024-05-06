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
  <path d="M16,30.36C8.082,30.36,1.64,23.918,1.64,16	S8.082,1.64,16,1.64S30.36,8.082,30.36,16S23.918,30.36,16,30.36z M16.36,26.045v3.591C23.716,29.444,29.64,23.4,29.64,16	c0-7.401-5.924-13.444-13.28-13.635v3.59l1.446,5.668l6.2-3.628l-3.629,6.2L27.456,16l-7.079,1.806l3.629,6.2l-6.2-3.629	L16.36,26.045z M15.64,2.365C8.285,2.556,2.36,8.599,2.36,16c0,7.4,5.925,13.444,13.28,13.636v-3.591l-1.446-5.668l-6.2,3.629	l3.628-6.2L4.543,16l7.079-1.806l-3.628-6.2l6.2,3.628l1.446-5.668C15.64,5.954,15.64,2.365,15.64,2.365z M14.655,19.273L16,24.544	l1.345-5.271l4.649,2.721l-2.721-4.649L24.544,16l-5.271-1.345l2.721-4.649l-4.649,2.721L16,7.457l-1.345,5.271l-4.649-2.721	l2.721,4.649L7.457,16l5.271,1.345l-2.721,4.649L14.655,19.273z"></path>
</svg>