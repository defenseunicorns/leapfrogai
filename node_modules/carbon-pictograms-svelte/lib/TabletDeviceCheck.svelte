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
  <path d="M14,17.509l-3.254-3.254l0.509-0.509L14,16.491l6.745-6.745l0.51,0.509L14,17.509z M17,28.5	c0-0.552-0.448-1-1-1s-1,0.448-1,1s0.448,1,1,1S17,29.052,17,28.5z M28.36,31V1c0-0.199-0.161-0.36-0.36-0.36H4	C3.801,0.64,3.64,0.801,3.64,1v30c0,0.199,0.161,0.36,0.36,0.36h24C28.199,31.36,28.36,31.199,28.36,31z M4.36,26.36h23.28v4.279	H4.36V26.36z M4.36,1.36h23.28v24.28H4.36V1.36z"></path>
</svg>