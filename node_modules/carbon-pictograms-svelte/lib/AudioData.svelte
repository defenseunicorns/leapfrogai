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
  <path d="M16,31.36C7.53,31.36,0.64,24.47,0.64,16	S7.53,0.64,16,0.64S31.36,7.53,31.36,16S24.47,31.36,16,31.36z M16,1.36C7.927,1.36,1.36,7.927,1.36,16	c0,8.072,6.567,14.64,14.64,14.64c8.072,0,14.64-6.567,14.64-14.64S24.072,1.36,16,1.36z M23.36,23h-0.72V9h0.721L23.36,23L23.36,23	z M11.36,23h-0.72V9h0.72V23z M17.36,21h-0.72V11h0.72V21z M8.36,20H7.64v-8h0.72V20z M26.36,19h-0.72v-6h0.721L26.36,19L26.36,19z M14.36,19h-0.72v-6h0.72V19z M20.36,17h-0.72v-2h0.721L20.36,17L20.36,17z M5.36,17H4.64v-2h0.72C5.36,15,5.36,17,5.36,17z"></path>
</svg>