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
  <path d="M16,31.36C7.53,31.36,0.64,24.47,0.64,16	S7.53,0.64,16,0.64S31.36,7.53,31.36,16S24.47,31.36,16,31.36z M16,1.36C7.927,1.36,1.36,7.927,1.36,16	c0,8.072,6.567,14.64,14.64,14.64c8.072,0,14.64-6.567,14.64-14.64S24.072,1.36,16,1.36z M16.36,29h-0.72v-5h0.72V29z M22,23.36h-5	v-0.72h5V23.36z M15,23.36h-5v-0.72h5V23.36z M16.36,22h-0.72v-5h0.72V22z M9.36,22H8.64v-5h0.72C9.36,17,9.36,22,9.36,22z M29,16.36h-5v-0.72h5V16.36z M22,16.36h-5v-0.72h5V16.36z M8,16.36H3v-0.72h5V16.36z M23.36,15h-0.72v-5h0.721L23.36,15L23.36,15z M16.36,15h-0.72v-5h0.72V15z M22,9.36h-5V8.64h5V9.36z M15,9.36h-5V8.64h5V9.36z M16.36,8h-0.72V3h0.72V8z"></path>
</svg>