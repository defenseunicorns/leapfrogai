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
  <path d="M31,31.36H21c-0.199,0-0.36-0.161-0.36-0.36v-1.64H16c-0.199,0-0.36-0.161-0.36-0.36V16.358	h-4.292C11.163,19.147,8.835,21.36,6,21.36c-2.956,0-5.36-2.405-5.36-5.36c0-2.956,2.404-5.36,5.36-5.36	c2.834,0,5.161,2.21,5.348,4.998h4.292V3c0-0.199,0.161-0.36,0.36-0.36l4.64-0.002V1c0-0.199,0.161-0.36,0.36-0.36h10	c0.199,0,0.36,0.161,0.36,0.36v4c0,0.199-0.161,0.36-0.36,0.36H21c-0.199,0-0.36-0.161-0.36-0.36V3.358l-4.28,0.001v12.278h4.28V14	c0-0.199,0.161-0.36,0.36-0.36h10c0.199,0,0.36,0.161,0.36,0.36v4c0,0.199-0.161,0.36-0.36,0.36H21c-0.199,0-0.36-0.161-0.36-0.36	v-1.642h-4.28V28.64h4.28V27c0-0.199,0.161-0.36,0.36-0.36h10c0.199,0,0.36,0.161,0.36,0.36v4C31.36,31.199,31.199,31.36,31,31.36z M21.36,30.64h9.279v-3.28H21.36V30.64z M6,11.36c-2.559,0-4.64,2.082-4.64,4.64S3.441,20.64,6,20.64s4.64-2.081,4.64-4.64	S8.559,11.36,6,11.36z M21.36,17.64h9.279v-3.28H21.36V17.64z M21.36,4.64h9.279V1.36H21.36V4.64z"></path>
</svg>