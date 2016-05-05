package main

import (
	"github.com/mkideal/cli"
)

var _ = publishCmd.Register(&cli.Command{
	Name: "us",
	Desc: "Publish golang application to US",
	Argv: func() interface{} { return new(publishUsT) },
	Fn:   publishUs,
})

type publishUsT struct {
	Help   bool   `cli:"h,help" usage:"display help information"`
	Dir    string `cli:"dir" usage:"source code root dir" dft:"./"`
	Suffix string `cli:"suffix" usage:"source file suffix" dft:".go,.c,.s"`
	Out    string `cli:"o,out" usage:"output filename"`
}

func publishUs(ctx *cli.Context) error {
	argv := ctx.Argv().(*publishUsT)

	if argv.Help {
		ctx.WriteUsage()
		return nil
	}
	ctx.String("%s: %v", ctx.Path(), jsonIndent(argv))
	return nil
}
