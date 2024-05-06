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
  <path d="M16,30.36C8.082,30.36,1.64,23.918,1.64,16	S8.082,1.64,16,1.64S30.36,8.082,30.36,16S23.918,30.36,16,30.36z M16,2.36C8.479,2.36,2.36,8.479,2.36,16S8.479,29.64,16,29.64	S29.64,23.522,29.64,16C29.64,8.479,23.521,2.36,16,2.36z M14.014,22.522l-4.268-4.268l0.509-0.51l3.732,3.732l8.746-9.718	l0.535,0.481L14.014,22.522z"></path>
</svg>