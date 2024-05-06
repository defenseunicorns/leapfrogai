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
  <path d="M16,31.36C8.082,31.36,1.64,24.918,1.64,17V1	c0-0.199,0.161-0.36,0.36-0.36h28c0.199,0,0.36,0.161,0.36,0.36v16C30.36,24.918,23.918,31.36,16,31.36z M2.36,1.36V17	c0,7.521,6.119,13.64,13.64,13.64S29.64,24.522,29.64,17V1.36h-6.28V16c0,4.059-3.302,7.36-7.36,7.36S8.64,20.058,8.64,16V1.36H2.36	z M9.36,1.36V16c0,3.661,2.979,6.64,6.64,6.64s6.64-2.979,6.64-6.64V1.36H9.36z"></path>
</svg>