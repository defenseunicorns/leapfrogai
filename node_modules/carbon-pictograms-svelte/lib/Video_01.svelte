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
  <path d="M23,27.36H1c-0.199,0-0.36-0.161-0.36-0.36V5c0-0.199,0.161-0.36,0.36-0.36h22	c0.199,0,0.36,0.161,0.36,0.36v6.375l7.459-4.331c0.11-0.064,0.248-0.066,0.36,0c0.111,0.064,0.181,0.183,0.181,0.312v17.321	c0,0.129-0.069,0.248-0.182,0.312c-0.11,0.063-0.249,0.063-0.36-0.002l-7.458-4.359V27C23.36,27.199,23.199,27.36,23,27.36z M1.36,26.64h21.28V20c0-0.129,0.069-0.248,0.182-0.312c0.11-0.063,0.25-0.063,0.36,0.002l7.458,4.359V7.98l-7.459,4.331	c-0.11,0.064-0.248,0.065-0.36,0C22.709,12.248,22.64,12.129,22.64,12V5.36H1.36V26.64z"></path>
</svg>