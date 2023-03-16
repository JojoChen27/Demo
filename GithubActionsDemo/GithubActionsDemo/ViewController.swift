//
//  ViewController.swift
//  GithubActionsDemo
//
//  Created by 陈超 on 2023/3/15.
//

import UIKit

extension String {
    func localized() -> String {
        if let path = Bundle.main.path(forResource: "en", ofType: "lproj"),
           let bundle = Bundle(path: path) {
            return bundle.localizedString(forKey: self, value: nil, table: "Localizable")
        }
        return self
    }

    func localizedFormat(_ arguments: CVarArg...) -> String {
        String(format: localized(), arguments: arguments)
    }
}

class ViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        title = "测试文本".localized() 
        title = "测试".localized()
        title = "测试1".localized()
        title = "测试3".localized()
        title = "测试4"
    }


}

