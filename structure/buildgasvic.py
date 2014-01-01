#!/usr/local/bin/pike

array(string) splitfn(string fn)
{
        sscanf(fn,"../html/shows/%d/%d%s",int year,int idx,string kwd);
        return ({sprintf("Season %d %d",idx,year),fn[14..]});
}

int main()
{
        multiset(string) has_index=(<"pirates","princessida","trial">),need_index=(<>);
        #ifdef FAKE
        string start=Process.run(({"git","rev-parse","fake_head"}))->stdout-"\n";
        #else
        string start=Process.run(({"git","rev-parse","HEAD"}))->stdout-"\n";
        Process.create_process(({"git","pull"}))->wait();
        #endif
        array(string) names=Process.run(({"git","diff","--name-only","-z",start+".."}))->stdout/"\0"-({""});
        array(string) rst2html=({"rst2html","--stylesheet-path=../html/gsvicwww.css","--link-stylesheet","--template=template.txt"}); //Standard args to rst2html
        foreach (names,string fn) if (has_suffix(fn,".rst"))
        {
                if (sscanf(fn,"index/%s",string part) && has_index[part]) {need_index[part]=1; continue;} //Do index files at the end.
                array(string) path=({"..","html"})+explode_path(fn);
                sscanf(path[-1],"%{%*[^a-z]%[a-z]%}",array(array(string)) parts); //Find out which index files need updating. A file name of "/asdf/1trial_sorcerer.rst" will check "trial","sorcerer","rst".
                foreach (parts*({}),string part) if (has_index[part]) need_index[part]=1;
                path[-1]=path[-1][..<4]+".html";
                string html=combine_path(@path);
                if (!file_stat(fn) && file_stat(html)) {rm(html); continue;}
                Stdio.mkdirhier(combine_path(@path[..<1]));
                Process.create_process(rst2html+({fn,html}))->wait();
        }
        array(string) allfiles=sizeof(need_index) && Process.run(({"find","../html/shows","-type","f","-print0"}))->stdout/"\0"-({""}); //Enumerate all files in all subdirectories... using an external command. This may want redoing, but hey, it's short.
        foreach (indices(need_index),string part)
        {
                //Rebuild the index, possibly also redo chain refs ("last time we did X" etc)
                string fn="index/"+part+".rst",html="../html/shows/"+part+".html";
                if (!file_stat(fn) && file_stat(html)) {rm(html); continue;}
                string content=sprintf("%{* `%s <%s>`__\n%}",map(filter(allfiles,has_value,part)-({html}),splitfn));
                mapping info=Process.run(rst2html,(["stdin":sprintf(Stdio.read_file(fn),content)]));
                if (info->stderr!="") werror(info->stderr);
                if (info->stdout!="") Stdio.File(html,"wct")->write(info->stdout); //If failure, leave previous content
        }
}

    Status
    API
    Training
    Shop
    Blog
    About

    � 2013 GitHub, Inc.
    Terms
    Privacy
    Security
    Contact

