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
  <path d="M14.5,21.5c0-0.828,0.672-1.5,1.5-1.5c0.828,0,1.5,0.672,1.5,1.5c0,0.704-0.487,1.29-1.14,1.452V25	c0,0.199-0.161,0.36-0.36,0.36s-0.36-0.161-0.36-0.36v-2.048C14.986,22.79,14.5,22.204,14.5,21.5z M26.355,13v18	c0,0.196-0.159,0.355-0.355,0.355H6c-0.196,0-0.355-0.159-0.355-0.355V13c0-0.196,0.159-0.355,0.355-0.355h4.64V6	c0-2.956,2.404-5.36,5.36-5.36S21.36,3.044,21.36,6h-0.72c0-2.559-2.081-4.64-4.64-4.64S11.36,3.442,11.36,6v6.645H26	C26.196,12.645,26.355,12.804,26.355,13z M25.645,13.355H6.355v17.289h19.289V13.355H25.645z"></path>
</svg>