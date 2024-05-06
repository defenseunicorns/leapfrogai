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
  <path d="M23.5,29.36h-15c-0.129,0-0.248-0.069-0.312-0.181l-7.5-13.01c-0.064-0.111-0.064-0.249,0-0.36	l7.5-12.99C8.252,2.708,8.372,2.64,8.5,2.64h15c0.129,0,0.247,0.068,0.312,0.18l7.5,12.99c0.064,0.111,0.064,0.249,0,0.36	l-7.5,13.01C23.748,29.291,23.629,29.36,23.5,29.36z M9.124,28.64h13.753L16,16.72L9.124,28.64z M16.618,16.35L23.5,28.279	l6.877-11.929C30.377,16.35,16.618,16.35,16.618,16.35z M1.623,16.35L8.5,28.279l6.882-11.929C15.382,16.35,1.623,16.35,1.623,16.35	z M16.629,15.63h13.747L23.5,3.72L16.629,15.63z M1.624,15.63h13.748L8.5,3.72L1.624,15.63z M9.124,3.36L16,15.28l6.877-11.92	C22.877,3.36,9.124,3.36,9.124,3.36z"></path>
</svg>