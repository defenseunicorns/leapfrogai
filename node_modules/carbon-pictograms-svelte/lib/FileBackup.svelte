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
  <path d="M16,31.36H1c-0.199,0-0.36-0.161-0.36-0.36V9c0-0.199,0.161-0.36,0.36-0.36h7.155V5	c0-0.199,0.161-0.36,0.36-0.36h7.125V1c0-0.199,0.161-0.36,0.36-0.36h15c0.199,0,0.36,0.161,0.36,0.36v22	c0,0.199-0.161,0.36-0.36,0.36h-7.124V27c0,0.199-0.161,0.36-0.36,0.36H16.36V31C16.36,31.199,16.199,31.36,16,31.36z M1.36,30.64	h14.28V9.36H1.36V30.64z M16.36,26.64h6.795V5.36H8.875v3.28H16c0.199,0,0.36,0.161,0.36,0.36V26.64z M23.876,22.64h6.764V1.36	H16.36v3.28h7.156c0.199,0,0.36,0.161,0.36,0.36C23.876,5,23.876,22.64,23.876,22.64z"></path>
</svg>