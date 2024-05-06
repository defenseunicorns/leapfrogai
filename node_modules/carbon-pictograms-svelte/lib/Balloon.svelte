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
  <path d="M19.36,31h-0.72c0-3.389-0.729-4.561-1.5-5.802	c-0.588-0.944-1.194-1.919-1.458-3.838H14.5c-0.136,0-0.261-0.077-0.322-0.199s-0.048-0.268,0.034-0.377l1.092-1.456	C11.019,18.931,7.64,14.899,7.64,10c0-5.161,3.75-9.36,8.36-9.36c4.609,0,8.36,4.199,8.36,9.36c0,4.899-3.379,8.931-7.665,9.328	l1.092,1.456c0.082,0.109,0.095,0.255,0.034,0.377c-0.062,0.122-0.186,0.199-0.322,0.199h-1.091c0.249,1.7,0.78,2.556,1.342,3.458	C18.542,26.09,19.36,27.405,19.36,31z M15.22,20.64h1.56L16,19.6L15.22,20.64z M16,1.36c-4.213,0-7.64,3.876-7.64,8.64	s3.427,8.64,7.64,8.64s7.64-3.875,7.64-8.64S20.213,1.36,16,1.36z M10.36,10H9.64c0-4.058,2.853-7.36,6.36-7.36v0.72	C12.89,3.36,10.36,6.339,10.36,10z"></path>
</svg>