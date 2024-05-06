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
  <path d="M29,31.36H3c-0.199,0-0.36-0.161-0.36-0.36V1c0-0.199,0.161-0.36,0.36-0.36h26c0.199,0,0.36,0.161,0.36,0.36	v30C29.36,31.199,29.199,31.36,29,31.36z M3.36,30.64h25.28V1.36H3.36V30.64z M16,24.36c-4.058,0-7.36-3.302-7.36-7.36	S11.942,9.64,16,9.64c4.059,0,7.36,3.302,7.36,7.36C23.36,21.059,20.059,24.36,16,24.36z M9.793,19.36	c0.954,2.499,3.376,4.279,6.207,4.279c2.83,0,5.253-1.78,6.207-4.279H9.793z M9.565,18.64h12.871	c0.134-0.524,0.204-1.074,0.204-1.64c0-3.661-2.979-6.64-6.64-6.64S9.36,13.339,9.36,17C9.36,17.565,9.431,18.115,9.565,18.64z M26,4.36h-6V3.64h6V4.36z"></path>
</svg>