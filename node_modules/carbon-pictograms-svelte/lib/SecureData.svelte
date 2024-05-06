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
  <path d="M16,31.36C8.082,31.36,1.64,24.918,1.64,17V1c0-0.199,0.161-0.36,0.36-0.36h28	c0.199,0,0.36,0.161,0.36,0.36v16C30.36,24.918,23.918,31.36,16,31.36z M16.36,26.361v4.274c3.757-0.099,7.14-1.723,9.552-4.274	H16.36z M2.36,1.36V17c0,7.4,5.925,13.444,13.28,13.636V1.36H2.36z M16.36,25.641h10.186c1.033-1.259,1.847-2.705,2.379-4.279H16.36	V25.641z M16.36,20.641h12.787c0.321-1.159,0.493-2.38,0.493-3.641v-0.64H16.36V20.641z M16.36,15.64h13.28v-4.28H16.36V15.64z M16.36,10.64h13.28V6.36H16.36V10.64z M16.36,5.64h13.28V1.36H16.36V5.64z"></path>
</svg>