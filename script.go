package main

import(
        "fmt"
        "runtime"
        "os"
        "os/exec"
        "math/rand"
        "time"
        "path"
)

var cmdLine_prefix string
var isLinux bool
var whitediff bool

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

func initial(){
        var(
                err error
        )
        checkOS()
        err =  os.Chdir(os.Args[1])
        if err != nil{
            fmt.Printf("Directory cannot find")
            os.Exit(1)
        }
        rand.Seed(time.Now().Unix())
}

func checkFileExistance() {
    Path := path.Join("solution" , "main_solution.cpp")
    _, err := os.Stat(Path)
    if os.IsNotExist(err) {
            fmt.Printf("Main solution missed\n")
            os.Exit(1)
    }
    _, err = os.Stat("generator.cpp")
    if os.IsNotExist(err) {
            fmt.Printf("Generator is missed\n")
            os.Exit(1)
    }
    _, err = os.Stat("validator.cpp")
    if os.IsNotExist(err) {
            fmt.Printf("Validator is missed\n")
            os.Exit(1)
    }
    _, err = os.Stat("checker.cpp")
    if os.IsNotExist(err) {
            whitediff = true
    } else {
            whitediff = false
    }
    _, err = os.Stat("data.json")
    if os.IsNotExist(err) {
            fmt.Printf("Json file is missed\n")
            os.Exit(1)
    }
}

func compilation() {
        exec.Command("g++" , "generator.cpp" , "-o" , path.Join("testcase" , "generator"))

}

func main(){
    //    var (
      //        err error
    //            file []string
      //  )
        initial()
        checkFileExistance() //check if important files exist or not
        //compilation()

}

