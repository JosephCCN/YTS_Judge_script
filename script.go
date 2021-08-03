package main

import(
        "fmt"
        "runtime"
        "os"
        "math/rand"
        "time"
)

var cmdLine_prefix string
var isLinux bool

func OSReadDir(root string) ([]string, error) {
        var files []string
        f, err := os.Open(root)
        if err != nil {
                return files, err
        }
        fileInfo, err := f.Readdir(-1)
        f.Close()
        if err != nil {
                return files, err
        }

        for _, file := range fileInfo {
                files = append(files, file.Name())
        }
        return files, nil
}


func checkOS(){
        if runtime.GOOS == "windows"{
                cmdLine_prefix = ""
                isLinux = false
        } else {
                cmdLine_prefix = "./"
                isLinux = true
        }
}

func init(){
        var(
                err error
        )
        checkOS()
        fmt.Printf("%s" , os.Args)
        err =  os.Chdir(os.Args[1])
        if err != nil{
            fmt.Printf("Directory cannot find")
            os.Exit(1)
        }
        rand.Seed(time.Now().Unix())
}

func main(){
        var (
                err error
                file []string
        )
        file, err = OSReadDir("solution")
        if err != nil{}
        fmt.Printf("%s" , file)
}

