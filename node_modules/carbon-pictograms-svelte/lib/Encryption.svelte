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
  <path fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width=".72" d="M10,21c0-3.314,2.686-6,6-6s6,2.686,6,6s-2.686,6-6,6S10,24.314,10,21z M16,11c-5.523,0-10,4.477-10,10s4.477,10,10,10	s10-4.477,10-10S21.523,11,16,11z M11,17.682V6c0-2.761,2.239-5,5-5s5,2.239,5,5v11.682 M16,22v2 M16,20c-0.552,0-1,0.448-1,1	s0.448,1,1,1s1-0.448,1-1S16.552,20,16,20z"></path>
</svg>