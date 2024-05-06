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
  <path d="M10.75,13c0,0.414-0.336,0.75-0.75,0.75S9.25,13.414,9.25,13s0.336-0.75,0.75-0.75	S10.75,12.586,10.75,13z M22,12.25c-0.414,0-0.75,0.336-0.75,0.75s0.336,0.75,0.75,0.75s0.75-0.336,0.75-0.75S22.414,12.25,22,12.25	z M16,31.36C7.53,31.36,0.64,24.47,0.64,16S7.53,0.64,16,0.64S31.36,7.53,31.36,16S24.47,31.36,16,31.36z M16,1.36	C7.927,1.36,1.36,7.927,1.36,16c0,8.072,6.567,14.64,14.64,14.64c8.072,0,14.64-6.567,14.64-14.64S24.072,1.36,16,1.36z M21.701,23.2c-0.02-0.028-1.952-2.84-5.701-2.84s-5.682,2.812-5.701,2.84L9.7,22.801c0.086-0.13,2.154-3.161,6.299-3.161	s6.214,3.031,6.3,3.161L21.701,23.2z"></path>
</svg>