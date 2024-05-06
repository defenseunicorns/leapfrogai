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
  <path d="M16,31.36C7.53,31.36,0.64,24.47,0.64,16S7.53,0.64,16,0.64S31.36,7.53,31.36,16S24.47,31.36,16,31.36z M15.64,28h0.72v2.636c7.788-0.188,14.087-6.488,14.276-14.276H28v-0.72h2.636C30.447,7.853,24.147,1.553,16.36,1.364V4h-0.72V1.364	C7.853,1.553,1.553,7.853,1.364,15.64H4v0.72H1.364c0.189,7.788,6.488,14.087,14.276,14.276V28z M22.748,20.312l-7.108-4.104V6h0.72	v9.792l6.748,3.896L22.748,20.312z"></path>
</svg>