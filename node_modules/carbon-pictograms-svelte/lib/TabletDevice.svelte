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
  <path d="M16,29.5c-0.552,0-1-0.448-1-1s0.448-1,1-1s1,0.448,1,1S16.552,29.5,16,29.5z M28.36,31V1	c0-0.199-0.161-0.36-0.36-0.36H4C3.801,0.64,3.64,0.801,3.64,1v30c0,0.199,0.161,0.36,0.36,0.36h24	C28.199,31.36,28.36,31.199,28.36,31z M4.36,26.36h23.28v4.279H4.36V26.36z M4.36,1.36h23.28v24.28H4.36V1.36z"></path>
</svg>